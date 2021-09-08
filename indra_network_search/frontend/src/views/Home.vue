<template>
  <div class="home">
    <NetworkSearchForm />
  </div>
</template>

<script>
// @ is an alias to /src
import NetworkSearchForm from "./NetworkSearchForm";

export default {
  name: "Home",
  components: {
    NetworkSearchForm,
  },
};
</script>
