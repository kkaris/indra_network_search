import "@popperjs/core/dist/cjs/popper";
import "bootstrap/dist/js/bootstrap.min";
import "@vueform/multiselect/themes/default.css";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap-icons/font/bootstrap-icons.css";
import "./assets/sources.css";
import { createApp, reactive } from "vue";
import App from "./App.vue";

const GStore = reactive(
    {
        currentQuery: {},
        xrefs: {},
    }
)

const app = createApp(App);
app.provide('GStore', GStore);
app.mount("#app");
