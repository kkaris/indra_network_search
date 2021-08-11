<template>
  <div class="form-floating">
    <input
      v-bind="$attrs"
      :id="strUUID"
      :value="modelValue"
      :placeholder="ph"
      :title="compTitle"
      :list="dataListID"
      @input="$emit('update:modelValue', $event.target.value)"
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
    getExternalAutoCompleteList() {
      // Call rest-api autocomplete //
      console.log('getExternalAutoCompleteList was called')

      // Check if search is allowed
      if (this.canSearch) {
        // Flag that we're waiting results to true and reset results to empty
        this.awaitingResults = true
        this.autoSearchResult = []
        let prefix = this.modelValue
        console.log('getExternalAutoCompleteList executed')
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
              console.log('getExternalAutoCompleteList setting awaitingResults to false')
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
    isPrefixOfPrefix() {
      // true if modelValue is a continuation of the most recent search
      if (this.modelValue.length > 0 && this.lastPrefixSearch.length > 0) {
        return this.modelValue.toLowerCase().startsWith(this.lastPrefixSearch.toLowerCase())
      }
      return false
    },
    canSearch() {
      // True if all conditions that allow for search are true
      return this.modelValue.length > 0 && !this.isPrefixOfPrefix && !this.awaitingResults
    },
  }
}
</script>
