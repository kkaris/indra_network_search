<template>
  <td class="border-end align-middle">
    <NodeModal v-bind="path[0]" />
    <template v-for="(nodeObj, index) in path.slice(1)" :key="index">
      <i class="bi bi-arrow-right"></i>
      <NodeModal v-bind="nodeObj"/>
    </template>
  </td>
  <td>
    <div class="container">
      <!-- Fixme: add some headers: edges, weight, support button, sources, linkout -->
      <div class="row">
        <div class="col text-nowrap text-end"><b>Weight</b></div>
        <div class="col-5"><b>Edge</b></div>
        <div class="col-4"><b>Sources</b></div>
        <div class="col"><b>DB Link</b></div>
      </div>
      <Edge
          v-for="(edge, index) in edge_data"
          :key="index"
          v-bind="edge"
          :show-weight="true"
      />
    </div>
  </td>
</template>

<script>
import sharedHelpers from "@/helpers/sharedHelpers";
import NodeModal from "@/components/Result/NodeModal";
import Edge from "@/components/Result/Edge";

export default {
  components: {Edge, NodeModal},
  props: {
    // Follows indra_network_search.data_models::Path
    path: {
      type: Array,
      required: true,
      validator: arr => {
        return sharedHelpers.isNodeArray(arr)
      }
    },
    edge_data: {
      type: Array,
      required: true,
      validator: arr => {
        return arr.length > 0;
      }
    }
  },
}
</script>
