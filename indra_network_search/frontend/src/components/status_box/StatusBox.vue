<template>
  <div class="container">
    show status and info
  </div>
</template>

<script>
export default {
  name: "StatusBox.vue",
  data() {
    return {
      // Follows indra_network_search.data_models.rest_models.ServerStatus
      unsigned_nodes: 0,
      signed_nodes: 0,
      unsigned_edges: 0,
      signed_edges: 0,
      status: '',
      graph_date: '',
    }
  },
  methods: {
    checkStatus() {
      // Call /status
      return {}
    }
  }
}
</script>

<style scoped>

</style>