<template>
  <div class="container" id="footer-container">
    <footer class="footer text-muted" id="about">
      <h5 class="my-0 mr-md-auto font-weight-normal fs-2" id="about-header">About</h5>
      <small>
        <ul class="list-unstyled justify-content-start">
          <li class="float-end">
            <a href="#">Back to top</a>
          </li>
          <li><a href="https://indralab.github.io" target="_blank">INDRALAB</a></li>
          <li><a href="http://hits.harvard.edu" target="_blank">Harvard Program in Therapeutic Science (HiTS)</a></li>
          <li><b>Automated Scientific Discovery Framework </b>(ASDF)</li>
          <li>The DARPA ASDF project develops algorithms and software for reasoning about complex mechanisms operating in the natural world, explaining large-scale data, assisting humans in generating actionable, model-based hypotheses and testing these hypotheses empirically.<br><i>ASDF is funded by the Defense Advanced Research Projects Agency under award W911NF018-1-0124.</i></li>
        </ul>
      </small>
    </footer>
  </div>
</template>

<script>
export default {
  name: "Footer.vue"
}
</script>

<style scoped>
#footer-container {
  background: #F5F5F5;
  text-align: start;
}

#about-header {
  text-align: center;
}
</style>