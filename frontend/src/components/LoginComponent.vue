<script setup>
import Cookies from "universal-cookie";
import { reactive, onMounted } from "vue";
import { useRouter } from 'vue-router'

const cookies = new Cookies()
const router = useRouter()

const formData = reactive({
  username: '',
  password: ''
})

const sessionView = () => {
  fetch("/session/", {
    credentials: "same-origin",
  })
    .then((res) => res.json())
}

const handleSubmit = () => {
  fetch("/login/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": cookies.get("csrftoken"),
    },
    credentials: "same-origin",
    body: JSON.stringify(formData),
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.detail === 'Successfully logged in.') {
        router.push({ name: 'Home' })
      }
    })
}

onMounted(() => {
  sessionView()
})
</script>

<template>
  <form @submit.prevent="handleSubmit" autocomplete="false" novalidate>
    <div class="mx-auto text-center" style="max-width: 400px;">
      <div class="mb-3">
        <label for="exampleInputUsername1" class="form-label">Username</label>
        <input type="text" class="form-control text-center" id="exampleInputUsername1" v-model="formData.username"
          aria-describedby="usernameHelp" />
      </div>
      <div class="mb-3">
        <label for="exampleInputPassword1" class="form-label">Password</label>
        <input type="password" class="form-control text-center" id="exampleInputPassword1" v-model="formData.password" />
      </div>
      <button type="submit" class="btn btn-outline-primary mt-3">Login</button>
    </div>
  </form>
</template>

<style scoped></style>
