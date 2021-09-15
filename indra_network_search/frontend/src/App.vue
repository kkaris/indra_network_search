<template>
  <HeaderInfo header="The INDRA Network Search"/>
  <div id="nav">
    <router-link to="/">Search</router-link> |
    <router-link to="/about">About</router-link>
  </div>
  <router-view />
  <AppFooter />
</template>

<script>
import HeaderInfo from "./components/header_info/HeaderInfo";
import AppFooter from "./components/app_footer/AppFooter";

export default {
  name: "App",
  components: {
    HeaderInfo,
    AppFooter,
  },
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav a {
  font-weight: bold;
}

#nav a.router-link-exact-active {
  color: #2c3e50;
}
</style>
