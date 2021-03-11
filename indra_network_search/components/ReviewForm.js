app.component('review-form', {
  template:
  /*html*/
  // .prevent in @submit.prevent prevents the default page reload of form
  // submission
  `<form class="review-form" @submit.prevent="onSubmit">
    <h3>Leave a review</h3>
    <label for="name">Name:</label>
    <input id="name" v-model="name">

    <label for="review">Review:</label>
    <textarea id="review" v-model="review"></textarea>

    <label for="rating">Rating:</label>
    <!-- v-model.number typecasts the value as a number -->
    <select id="rating" v-model.number="rating">
      <option>5</option>
      <option>4</option>
      <option>3</option>
      <option>2</option>
      <option>1</option>
    </select>

    <p>Would you recommend this product?</p>
    <input v-model="recommendYes" type="radio" id="yes" name="recommend" value="yes"/>
    <label for="yes">Yes</label>
    <input v-model="recommendNo" type="radio" id="no" name="recommend" value="no"/>
    <label for="no">No</label>

    <input class="button" type="submit" value="Submit">
  </form>`,
  data() {
    return {
      name: '',
      review: '',
      rating: null,
      recommendYes: '',
      recommendNo: ''
    }
  },
  methods: {
    onSubmit() {
      if (this.name === '' || this.review === '' || this.rating === null ||
        (this.recommendYes === '' && this.recommendNo === '')) {
        alert('Review is incomplete. Please fill out every field.')
        return
      }

      let productReview = {
        name: this.name,
        review: this.review,
        rating: this.rating,
        recommend: this.recommendYes || this.recommendNo
      }
      //         event name          event payload
      this.$emit('review-submitted', productReview)

      this.name = ''
      this.review = ''
      this.rating = null
      this.recommendYes = ''
      this.recommendNo = ''
    }
  }
})