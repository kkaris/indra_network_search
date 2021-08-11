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
      type: [String, Number],
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
      lastPrefix: '',
      searchName: '',
      autoSearchResult: [
        ['MAPK1', 'HGNC', '6871'],
        ['Mapk1', 'UP', 'P63085'],
        ['Mapk10', 'UP', 'P49187'],
        ['Mapk11', 'UP', 'Q9WUI1'],
        ['Mapk12', 'UP', 'Q63538'],
        ['Mapk13', 'UP', 'Q9Z1B7'],
        ['Mapk14', 'UP', 'P47811'],
        ['mapk14a', 'UP', 'Q9DGE2'],
        ['MAPK15', 'HGNC', '24667'],
        ['Mapk1ip1', 'UP', 'Q9D7G9'],
        ['MAPK1IP1L', 'HGNC', '19840'],
      ],
    }
  },
  methods: {
    // todo: make even faster by providing an internal autocomplete of data already existing
    getExternalAutoCompleteList() {
      // Call rest-api autocomplete
      AxiosMethods.auto(this.modelValue)
      .then(response => {
        console.log(response)
      })
      // this.autoSearchResult =
    },
    getInternalAutoCompleteList() {
      // Autocomplete from already saved list
      return []
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
    autoSearchNames() {
      return this.autoSearchResult.map(t => t[0])
    }
  }
}
</script>
