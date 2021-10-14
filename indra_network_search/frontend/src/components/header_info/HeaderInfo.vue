<template>
  <h1 class="text-center">{{ header }}</h1>
  <p class="text-center align-items-center">
    <template v-if="unsigned_nodes && unsigned_edges"
      >Search across {{ unsigned_nodes }} nodes,
      {{ unsigned_edges }} edges.<br></template
    >
    <template v-if="graph_date">Last updated: {{ graph_date }}.</template>
    Server Status: <span class="badge" :class="badgeClass">{{ status }}</span>
  </p>
</template>

<script>
import AxiosMethods from "../../services/AxiosMethods";

export default {
  name: "HeaderInfo.vue",
  props: {
    header: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      response: {},
      serverError: false,
    };
  },
  computed: {
    // Follows indra_network_search.data_models.rest_models.ServerStatus
    unsigned_nodes() {
      return this.response && this.response.unsigned_nodes
        ? this.response.unsigned_nodes
        : null;
    },
    signed_nodes() {
      return this.response && this.response.signed_nodes
        ? this.response.signed_nodes
        : null;
    },
    unsigned_edges() {
      return this.response && this.response.unsigned_edges
        ? this.response.unsigned_edges
        : null;
    },
    signed_edges() {
      return this.response && this.response.signed_edges
        ? this.response.signed_edges
        : null;
    },
    status() {
      return this.response && this.response.status
        ? this.response.status
        : "unknown";
    },
    graph_date() {
      return this.response && this.response.graph_date
        ? this.response.graph_date
        : "";
    },
    badgeClass() {
      if (this.serverError) {
        return "server-error";
      } else if (this.response && this.response.status === "available") {
        return "server-available";
      }
      return "server-other";
    },
    circleClass() {
      if (this.serverError) {
        return "server-error-sm";
      } else if (this.response && this.response.status === "available") {
        return "server-available-sm";
      }
      return "server-other-sm";
    },
  },
  mounted() {
    // FixMe: Created might be more suitable?
    this.checkStatus();
  },
  methods: {
    checkStatus() {
      this.serverError = false;
      AxiosMethods.checkServerStatus()
        .then((response) => {
          this.response = response.data;
        })
        .catch((error) => {
          console.log(error);
          this.serverError = true;
        });
    },
  },
};
</script>

<style scoped>
.server-available {
  background-color: #00a000;
  color: white;
}
.server-available-sm {
  color: #00a000;
}
.server-other {
  background-color: #1f78b4;
  color: white;
}
.server-other-sm {
  color: #1f78b4;
}
.server-error {
  background-color: #ac2925;
  color: white;
}
.server-error-sm {
  color: #ac2925;
}
</style>
