<template>
  <div class="form-floating">
    <input
      v-bind="$attrs"
      :id="strUUID"
      :value="modelValue"
      :placeholder="ph"
      :title="compTitle"
      :list="dataListID"
      @input="$emit('update:modelValue', $event.target.value), getExternalAutoCompleteList($event.target.value)"
      type="search"
      class="form-control"
      :class="{ 'is-valid': isValidNode }"
    >
    <label :for="strUUID" class="form-label" v-if="label">{{ label }}</label>
    <datalist :id="dataListID">
      <option
          v-for="(searchArr, index) in autoSearchResult"
          :key="index"
          :value="searchArr[0]"
      >{{ `${searchArr[1]}:${searchArr[2]}`}}
      </option>
    </datalist>
    <template v-if="errors.length > 0">
      <p
          v-for="error in errors"
          :key="error.$uid"
          style="color: #A00000">
        {{ error.$message ? error.$message : 'Invalid entry' }}
      </p>
    </template>
  </div>
</template>

<script>
import UniqueID from "../../helpers/BasicHelpers";
import AxiosMethods from "../../services/AxiosMethods";
export default {
  name: "BaseInputAutoCompBS.vue",
  props: {
    label: {
      type: String,
      default: ''
    },
    modelValue: {
      type: String,
      default: ''
    },
    placeholder: {
      type: String,
      default: ''
    },
    title: {
      type: String,
      default: ''
    },
    errors: {
      type: Array,
      default: () => {
        return []
      }
    }
  },
  data() {
    return {
      lastPrefixSearch: '',
      autoSearchResult: [],
      awaitingResults: false,
    }
  },
  methods: {
    isPrefixOfPrefix(value) {
      if (value.length > 0 && this.lastPrefixSearch.length > 0) {
        // true if value is a continuation of the most recent search OR
        // is *not* value='chebi:', lastPrefixSearch='chebi' i.e. a prefix search
        return value.toLowerCase().startsWith(this.lastPrefixSearch.toLowerCase())
      }
      return false
    },
    isActuallyNSIDSearch(value) {
      // Search is for ns:id if
      // - string includes ':' &&
      // - previous search does not include ':' &&
      // - current value does not end with ':', i.e. don't search all entities within a prefix
      return value.includes(':') && !this.lastPrefixSearch.includes(':') && !value.endsWith(':')
    },
    canSearch(value) {
      // True if all conditions that allow for search are true
      // 1 or 2 letter prefix searches do exact matches,
      // so a 2 or 3+ letter prefix needs to be searched again
      return value.length > 0 &&
          (!this.isPrefixOfPrefix(value) ||
              this.lastPrefixSearch.length <= 2 ||
              this.isActuallyNSIDSearch(value)) &&
          !this.awaitingResults
    },
    getExternalAutoCompleteList(value) {
      // Call rest-api autocomplete //

      // Check if search is allowed
      if (this.canSearch(value)) {
        // Flag that we're waiting results to true and reset results to empty
        this.awaitingResults = true
        this.autoSearchResult = []
        let prefix = value
        // ToDo: make async
        AxiosMethods.auto(prefix)
            .then(response => {
              this.lastPrefixSearch = prefix
              console.log(`Got response for prefix search ${prefix}`)
              this.autoSearchResult = response.data
            })
            .catch(error => {
              console.log('getExternalAutoCompleteList errored')
              console.log(error)
            })
            .then(() => {
              // console.log('getExternalAutoCompleteList setting awaitingResults to false')
              this.awaitingResults = false
            })
      }
    }
  },
  setup() {
    const uuid = UniqueID().getID();
    return {
      uuid
    }
  },
  computed: {
    strUUID() {
      return `autocomplete${this.uuid}`
    },
    dataListID() {
      return `datalist${this.strUUID}`
    },
    ph() {
      return this.placeholder || this.label
    },
    compTitle() {
      return this.title || this.ph
    },
    isValidNode() {
      // Check if modelValue is among the names in autoSearchNames
      return this.autoSearchResult.map(t => t[0]).includes(this.modelValue)
    },
  }
}
</script>
