<template>
  <span class="source-display">
    <span v-for="(src_group, cat, idx) in sources" :key="cat">
      <span
          v-if="idx > 0"
          style="color: #212529;"
          class="badge badge-source">|</span>
      <span v-for="src in src_group"
            :key="src">
        <template v-if="src === 'fplx' && showSrc(src)">
          <span title="ontological edge">
            <i class="bi bi-diagram-2"></i>
          </span>
        </template>
        <template v-else>
        <span
            :class="`${badgeClass} source-${src}`"
            v-if="showSrc(src)"
            :title="src">
          <span v-if="source_counts">
            {{ source_counts[src] }}
          </span>
          <span v-else>
            {{ src }}
          </span>
        </span>
        </template>
      </span>
    </span>
  </span>
</template>

<script>
import sourceList from '../../assets/source_list.json';
  export default {
    name: "SourceDisplay",
    props: {
      source_counts: {
        type: Object,
        default: null
      }
    },
    methods: {
      showSrc: function(src) {
        if (this.source_counts === null)
          return true;
        if ( !(src in this.source_counts) )
          return false;
        else if ( this.source_counts[src] > 0 )
          return true;
        return false;
      },
    },
    data() {
      return {
        sources: sourceList,
      }
    },
    computed: {
      badgeClass: function() {
        let base = 'badge badge-source';
        if (this.source_counts === null)
          return  base + ' label';
        else
          return base;
      }
    }
  }
</script>

<style scoped>
  .label {
    margin: 1px;
  }
</style>