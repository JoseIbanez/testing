<template>
  <img alt="Vue logo" src="./assets/logo.png" />
  <h2>Hello Vue 3 in CodeSandbox!</h2>

  <form @submit="onSubmit" class="add-form">
    <div class="form-control">
      <label>email</label>
      <input
        type="email"
        v-model="email"
        name="email"
        placeholder="Enter your email"
      />
    </div>

    <div class="form-control">
      <label>Comment</label>
      <input
        type="text"
        v-model="comment"
        name="comment"
        placeholder="Enter your comment"
      />
    </div>

    <input type="submit" value="Submit" class="btn btn-block" />
  </form>
</template>



<script>
import axios from "axios";

export default {
  name: "AddInformation",
  data() {
    return {
      email: "",
      comment: "",
    };
  },
  methods: {
    onSubmit(e) {
      e.preventDefault();

      if (!this.email) {
        alert("Please add some comment");
        return;
      }

      const newInformation = {
        Id: Math.floor(Math.random() * 10000000).toString(),
        Email: this.email,
        Comment: this.comment,
      };

      this.$emit("add-information", newInformation);
      console.log("sending ... ", newInformation);

      axios
        .post(process.env.VUE_APP_API_URL+"/api/feedback", newInformation, {
        headers: { 
          'Access-Control-Allow-Origin' : '*'
        }})
        .then((response) => console.log(response))
        .catch((error) => console.log(error));

      this.name = "";
      this.age = "";
    },
  },
};
</script>



<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
