"""Serves the frontend

Todo: This services provides a frontend to what was previously done in
 python script
 Consider hosting the data directory (from the subservices) here as well
 instead of calling that service (can be good to if you just want to test
 the JS approach without running all the services)
"""
import json
import logging
from os import environ
from typing import Optional

from pydantic import BaseModel
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from indra.statements.agent import default_ns_order as NS_LIST_
from indra_network_search.data_models import NetworkSearchQuery
from indra_network_search.net_util import *
from indra_network_search.util import *
from indra_network_search.net import IndraNetwork, EMPTY_RESULT

logger = logging.getLogger(__name__)


# defined here to not have possible import conflicts
class Job(BaseModel):
    """Defines a job"""
    id: str
    status: str
    query: NetworkSearchQuery
    job_status: JobStatus


app = FastAPI()
app.mount('/static', StaticFiles(directory=STATIC), name='static')
app.mount('/vue', StaticFiles(directory=API_PATH), name='vue')
templates = Jinja2Templates(directory=TEMPLATES)
data_dir = '/home/klas/repos/fastapi_test/examples/data'
app.mount('/data', StaticFiles(directory=data_dir), name='data')

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

# Fixme: This should not be here, replace with service health check
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
