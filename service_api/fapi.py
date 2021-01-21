"""Serves the frontend


Todo: This services provides a frontend to what was previously done in
 python script
 Consider hosting the data directory (from the subservices) here as well
 instead of calling that service (can be good to if you just want to test
 the JS approach without running all the services)
"""
import requests
from os import environ
from typing import Dict
from indra.statements.agent import default_ns_order as NS_LIST_
from depmap_analysis.util.aws import check_existence_and_date_s3, \
    read_query_json_from_s3

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from indra_network_service.indra_network.indra_network_util import *
from .util import *

from indra_network_service.indra_network.indra_network import IndraNetwork, \
    EMPTY_RESULT


class Job(BaseModel):
    """Defines a job"""
    id: str
    status: str
    query: NetworkSearchQuery
    job_status: JobStatus


app = FastAPI()
app.mount('/static', StaticFiles(directory=STATIC), name='static')
templates = Jinja2Templates(directory=TEMPLATES)

logger = logging.getLogger(__name__)

INDRA_DB_FROMAGENTS = 'https://db.indra.bio/statements/from_agents'
INDRA_DB_HASHES_URL = 'https://db.indra.bio/statements/from_hashes'
STMTS_FROM_HSH_URL = environ.get('INDRA_DB_HASHES_URL', INDRA_DB_HASHES_URL)
VERBOSITY = int(environ.get('VERBOSITY', 0))
API_DEBUG = int(environ.get('API_DEBUG', 0))

if API_DEBUG:
    logger.info('API_DEBUG set to %d' % API_DEBUG)
    SERVICE_BASE_URL = 'http://localhost:8000'
else:
    SERVICE_BASE_URL = 'https://network.indra.bio'

# Fixme: This should not be here
indra_network = IndraNetwork()


@app.get('/health')
async def health():
    """Check health on service"""
    # ToDo async call main service, that in turn calls sub services
    return {'status': 'pass'}


@app.get('/', response_class=HTMLResponse)
async def query_page(request: Request, query: Optional[int] = None):
    """Loads or responds to queries submitted on the query page"""
    logger.info('Got query')
    # logger.info('Incoming Args -----------')
    # logger.info(repr(request.args))

    stmt_types = get_queryable_stmt_types()
    has_signed_graph = len(indra_network.signed_nodes) > 0

    # Get query hash from parameters
    qh = query
    if qh:
        # Get query hash
        logger.info('Got query hash %s' % str(qh))
        old_results = check_existence_and_date_s3(qh)

        # Get result json
        res_json_key = old_results.get('result_json_key')
        results_json = read_query_json_from_s3(res_json_key) if res_json_key\
            else {}

        # Get query json
        query_json_key = old_results.get('query_json_key')
        query_json = read_query_json_from_s3(query_json_key) if \
            query_json_key else {}

        source = query_json.get('source', '')
        target = query_json.get('target', '')
    else:
        results_json = {'result': EMPTY_RESULT}
        query_json = {}
        source = ''
        target = ''
    return templates.TemplateResponse(
        'fast_api_query_template.html',
        context={
            'request': request,
            'query_hash': qh,
            'stmt_types': stmt_types,
            'node_name_spaces': list(NS_LIST_),
            'terminal_name_spaces': list(NS_LIST),
            'has_signed_graph': has_signed_graph,
            'old_result': json.dumps(results_json),
            'old_query': json.dumps(query_json),
            'source': source,
            'target': target,
            'indra_db_url_fromagents': INDRA_DB_FROMAGENTS
        })


# Todo make aiohttp
def get_hosted_file(qh: str, _type: str) -> Dict:
    res = requests.get(f'http://localhost:8000/data/{qh}_{_type}.json')
    res.raise_for_status()
    if res.status_code == 200:
        return res.json()


# Make a depends-on here for both the actual result and the meta file
# TodO: this could be replaced in the future with Vue querying S3 or this
#  service querying S3
@app.get('/data/{qh}_meta.json', response_model=JobStatus)
def read_meta_file(qh: str):
    return get_hosted_file(qh, 'meta')


@app.get('/data/{qh}_result.json', response_model=QueryResult)
def read_result_file(qh: str):
    return get_hosted_file(qh, 'result')
