import { createRouter, createWebHashHistory } from "vue-router";
import NetworkSearchForm from "../views/NetworkSearchForm";
import About from "../views/About"

const routes = [
  {
    path: "/",
    name: "NetworkSearch",
    component: NetworkSearchForm,
  },
  {
    path: "/about",
    name: "About",
    component: About,
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited. This improves
    // performance if the app becomes very large.
    // component: () =>
    //   import(/* webpackChunkName: "about" */ "../views/About.vue"),
  },
];

const router = createRouter({
  history: createWebHashHistory(process.env.BASE_URL),
  routes,
});

export default router;
