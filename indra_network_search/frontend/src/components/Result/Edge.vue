<template>
  <div class="container">
    <div class="row d-flex justify-content-center">
      <div class="col-5">
        <NodeModal v-bind="subjNode" />
        <i class="bi bi-arrow-right"></i>
        <NodeModal v-bind="objNode" />
      </div>
      <div class="col text-start">
        <a
          role="button"
          class="text-reset"
          data-bs-toggle="collapse"
          :href="`#${strUUID}`"
          :aria-expanded="false"
          :aria-controls="strUUID"
          @click="toggleShowFlag()"
        >
          <i v-if="isExpanded" title="Click to collapse" class="bi-dash-circle"></i>
          <i v-else title="Click to expand" class="bi-plus-circle"></i>
        </a><b v-if="showWeight">{{ weightToShow }}</b>
      </div>
      <div class="col-5 text-end">
        <SourceDisplay :source_counts="source_counts" />
      </div>
      <div class="col">
        <span>
          <a :href="db_url_edge">
            <i class="bi bi-box-arrow-up-right"></i>
          </a>
        </span>
      </div>
    </div>
    <div class="row collapse" :id="strUUID">
      <EdgeSupport
          :subj-node="subjNode"
          :obj-node="objNode"
          :stmt-data-obj="statements"
      />
    </div>
  </div>
</template>

<script>
import NodeModal from "@/components/Result/NodeModal";
import EdgeSupport from "@/components/Result/EdgeSupport";
import sharedHelpers from "@/helpers/sharedHelpers";
import UniqueID from "@/helpers/BasicHelpers";
import SourceDisplay from "@/components/Result/SourceDisplay";
export default {
  components: {SourceDisplay, EdgeSupport, NodeModal},
  props: {
    // Follows BaseModel indra_network_search.data_models::EdgeData
    edge: {
      // List[Node] - Edge supported by statements
      type: Array,
      required: true,
      validator: arr => {
        const arrLen = arr.length > 0;
        const containsNodes = arr.every(sharedHelpers.isNode);

        return arrLen && containsNodes
      }
    },
    statements: {
      // Dict[str, StmtTypeSupport] - key by stmt_type
      type: Object,
      required: true,
      validator: obj => {
        return Object.keys(obj).length > 0;
      }
    },
    belief: {
      type: Number,
      required: true
    },
    weight: {
      type: Number,
      required: true
    },
    sign: {
      type: Number,
      default: null
    },
    context_weight: {
      type: [Number, String],
      default: 'N/A'
    },
    db_url_edge: {
      type: String,
      required: true
    },
    source_counts: {
      type: Object,
      required: true,
      validator: obj => {
        return sharedHelpers.isSourceCount(obj)
      }
    },
    showWeight: {
      type: Boolean,
      default: false
    }
  },
  setup() {
    const uuid = UniqueID().getID();
    return {
      uuid
    }
  },
  methods: {
    toggleShowFlag() {
      this.isExpanded = !this.isExpanded
    }
  },
  data() {
    return {
      isExpanded: false // FixMe: how to read the value set in the tags?
    }
  },
  computed: {
    subjNode() {
      return this.edge[0]
    },
    objNode() {
      return this.edge[1]
    },
    strUUID() {
      return `collapse-${this.uuid}`
    },
    isCollapsed() {
      return !document.getElementById(this.strUUID).classList.contains('show')
    },
    contextWeightFixed() {
      if (this.context_weight.toLowerCase() === 'n/a') {
        return this.context_weight
      }
      try {
        return Number(this.context_weight).toFixed(2)
      } catch (err) {
        try {
          // Find index of '.'
          const decIndex = this.context_weight.indexOf('.') + 3
          return this.context_weight.slice(0, decIndex);
        } catch (err) {
          return this.context_weight;
        }
      }
    },
    weightToShow() {
      // If context weighted is not "N/A", return regular weight
      if (this.context_weight.toLowerCase() === 'n/a') {
        return this.weight
      }
      return this.context_weight
    }
  }
}
</script>
