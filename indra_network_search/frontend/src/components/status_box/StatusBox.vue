<template>
  <div class="card">
    <h5 class="card-header">Service Status</h5>
    <div class="card-body">
      <ul class="list-group">
        <li
            v-if="status"
            class="list-group-item d-flex justify-content-between align-items-center"
        >Status
          <span class="badge" :class="badgeClass">{{ status }}</span>
        </li>
        <li
            v-if="graph_date"
            class="list-group-item d-flex justify-content-between align-items-center"
        >Date
          <span class="badge bg-secondary">{{ graph_date }}</span>
        </li>
        <li
            v-if="unsigned_nodes"
            class="list-group-item d-flex justify-content-between align-items-center"
        >Nodes
          <span class="badge bg-primary rounded-pill">{{ unsigned_nodes }}</span>
        </li>
        <li
            v-if="unsigned_edges"
            class="list-group-item d-flex justify-content-between align-items-center"
        >Edges
          <span class="badge bg-primary rounded-pill">{{ unsigned_edges }}</span>
        </li>
        <li
            v-if="signed_nodes"
            class="list-group-item d-flex justify-content-between align-items-center"
        >Signed nodes
          <span class="badge bg-primary rounded-pill">{{ signed_nodes }}</span>
        </li>
        <li
            v-if="signed_edges"
            class="list-group-item d-flex justify-content-between align-items-center"
        >Signed edges
          <span class="badge bg-primary rounded-pill">{{ signed_edges }}</span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import AxiosMethods from "../../services/AxiosMethods";
export default {
  name: "StatusBox.vue",
  data() {
    return {
      response: {},
      serverError: false
    }
  },
  computed: {
    // Follows indra_network_search.data_models.rest_models.ServerStatus
    unsigned_nodes() {
      return this.response && this.response.unsigned_nodes ? this.response.unsigned_nodes : null
    },
    signed_nodes() {
      return this.response && this.response.signed_nodes ? this.response.signed_nodes : null
    },
    unsigned_edges() {
      return this.response && this.response.unsigned_edges ? this.response.unsigned_edges : null
    },
    signed_edges() {
      return this.response && this.response.signed_edges ? this.response.signed_edges : null
    },
    status() {
      return this.response && this.response.status ? this.response.status : 'unknown'
    },
    graph_date() {
      return this.response && this.response.graph_date ? this.response.graph_date : ''
    },
    badgeClass() {
      if (this.serverError) {
        return 'server-error'
      } else if (this.response && this.response.status === 'available') {
        return 'server-available'
      }
      return 'server-other'
    }
  },
  mounted() {
    this.checkStatus()
  },
  methods: {
    checkStatus() {
      this.serverError = false
      AxiosMethods.checkServerStatus()
          .then(response => {
            this.response = response.data
          })
          .catch(error => {
            console.log(error)
            this.serverError = true;
          })
    }
  }
}
</script>

<style scoped>
  .server-available {
    background-color: #00A000;
    color: white;
  }
  .server-other {
    background-color: #1f78b4;
    color: white;
  }
  .server-error {
    background-color: #ac2925;
    color: white;
  }
</style>