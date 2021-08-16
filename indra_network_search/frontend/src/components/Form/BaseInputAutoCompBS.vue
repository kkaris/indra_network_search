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
    <p v-if="modelValue.endsWith(':')">Add a character to search for entities present from "{{ modelValue.toLowerCase().slice(0, modelValue.length-1) }}"</p>
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
    containsResult(nameNSIDTuple) {
      const name = nameNSIDTuple[0]
      for (let res of this.autoSearchResult) {
        if (res[0] === name) {
          return true
        }
      }
      return false
    },
    appendResults(resArray) {
      for (let item in resArray) {
        if (!this.containsResult(item)) {
          this.autoSearchResult.push(item)
        }
      }
    },
    isContinuedSearch(value) {
      /* Defines if a new value is simply more typing another letter
      to sort among already received results */
      return this.lastPrefixSearch.length > 0 &&
          value.toLowerCase().startsWith(this.lastPrefixSearch.toLowerCase()) &&
          value.length > 3 && // 1 and 2 letter prefixes do exact matching so 3 need new search, while 4 could be new search
          Math.abs(value.length - this.lastPrefixSearch.length) <= 1 // Jumps in length between searches could indicate copy pasting to replace the latest search
    },
    canSearch(value) {
      // Check conditions that allow for a search to take place
      return value.length > 0 && // There is a value
          !this.awaitingResults && // Search is currently not being done
          (!this.isContinuedSearch(value) || // Either started typing something new e.g. 'abc' -> 'xyz'
              (this.isContinuedSearch(value) && this.autoSearchResult.length >= 100) || // or need more results
              value.endsWith(':')) // or this is an NS:ID search and only
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
      // false if nothing entered
      if (!this.modelValue) {
        return false
      // false if we're waiting for results
      } else if (this.awaitingResults) {
        return false
      }
      // true if among results with case match
      return this.autoSearchResult.length && this.autoSearchResult.map(t => t[0]).includes(this.modelValue)
    },
  }
}
</script>
