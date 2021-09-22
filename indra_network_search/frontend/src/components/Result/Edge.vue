<template>
  <div class="row d-flex justify-content-center">
    <div class="col text-start text-nowrap">
      <a
        role="button"
        class="text-reset"
        data-bs-toggle="collapse"
        :href="`#${strUUID}`"
        :aria-expanded="false"
        :aria-controls="strUUID"
        @click="toggleShowFlag()"
      >
        <i
          v-if="isExpanded"
          title="Click to collapse"
          class="bi-dash-circle"
        ></i>
        <i v-else title="Click to expand" class="bi-plus-circle"></i>
      </a>
      &nbsp;
      <b title="Edge weight" v-if="showWeight">{{ weightToShow }}</b>
    </div>
    <div class="col-5">
      <NodeModal v-bind="subjNode" />
      <i class="bi bi-arrow-right"></i>
      <NodeModal v-bind="objNode" />
    </div>
    <div class="col-4 text-end">
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
</template>

<script>
import NodeModal from "@/components/Result/NodeModal";
import EdgeSupport from "@/components/Result/EdgeSupport";
import sharedHelpers from "@/helpers/sharedHelpers";
import UniqueID from "@/helpers/BasicHelpers";
import SourceDisplay from "@/components/Result/SourceDisplay";
export default {
  inject: ["GStore"],
  components: { SourceDisplay, EdgeSupport, NodeModal },
  props: {
    // Follows BaseModel indra_network_search.data_models::EdgeData
    edge: {
      // List[Node] - Edge supported by statements
      type: Array,
      required: true,
      validator: (arr) => {
        const arrLen = arr.length > 0;
        const containsNodes = arr.every(sharedHelpers.isNode);

        return arrLen && containsNodes;
      },
    },
    statements: {
      // Dict[str, StmtTypeSupport] - key by stmt_type
      type: Object,
      required: true,
      validator: (obj) => {
        return Object.keys(obj).length > 0;
      },
    },
    belief: {
      type: Number,
      required: true,
      validator: (b) => {
        return 0 <= b <= 1;
      },
    },
    weight: {
      type: Number,
      required: true,
      validator: (w) => {
        return sharedHelpers.isPosNum(w);
      },
    },
    context_weight: {
      type: [Number, String],
      default: "N/A",
      validator: (cw) => {
        return cw === "N/A" || sharedHelpers.isPosNum(cw);
      },
    },
    z_score: {
      type: Number,
      default: null,
    },
    corr_weight: {
      type: Number,
      default: null,
      validator: (corr) => {
        if (corr !== null) {
          // Assert gt 0
          return corr > 0;
        }
        return true;
      },
    },
    sign: {
      type: Number,
      default: null,
      validator: (s) => {
        if (s !== null) {
          return s === 0 || s === 1;
        }
        return true;
      },
    },
    db_url_edge: {
      type: String,
      required: true,
    },
    source_counts: {
      type: Object,
      required: true,
      validator: (obj) => {
        return sharedHelpers.isSourceCount(obj);
      },
    },
    // Flag whether the edge should display weight at all
    showWeight: {
      type: Boolean,
      default: false,
    },
  },
  setup() {
    const uuid = UniqueID().getID();
    return {
      uuid,
    };
  },
  methods: {
    toggleShowFlag() {
      this.isExpanded = !this.isExpanded;
    },
    fixDecimals(num, fractionDigits = 2) {
      try {
        return Number(num).toFixed(fractionDigits);
      } catch (err) {
        try {
          // Find index of '.'
          const decIndex = num.indexOf(".") + 3;
          // Slice to get two decimals
          return num.slice(0, decIndex);
        } catch (err) {
          return num;
        }
      }
    },
  },
  data() {
    return {
      isExpanded: false, // FixMe: how to read the value set in the tags?
    };
  },
  computed: {
    subjNode() {
      return this.edge[0];
    },
    objNode() {
      return this.edge[1];
    },
    strUUID() {
      return `collapse-${this.uuid}`;
    },
    isCollapsed() {
      return !document.getElementById(this.strUUID).classList.contains("show");
    },
    isContextWeighted() {
      return (
        !this.GStore.currentQuery.strict_mesh_id_filtering &&
        this.GStore.currentQuery.mesh_ids.length > 0
      );
    },
    weightToShow() {
      let weightType = this.GStore.currentQuery.weighted;

      switch (weightType) {
        case "unweighted":
          return "N/A"
        case "belief":
          return this.fixDecimals(this.weight);
        case "context":
          if (this.isContextWeighted) {
            return this.fixDecimals(this.context_weight);
          }
          return "N/A";
        case "z_score":
          return this.fixDecimals(this.corr_weight);
        default:
          throw `Unrecognized weight type ${weightType}`;
      }
    },
  },
};
</script>
