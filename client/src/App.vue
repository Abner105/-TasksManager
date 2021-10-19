<template>
  <div id="app">
    <!-- <button>修改</button>
    <button>添加</button> -->
    <router-link to="/tasks">任务列表</router-link>
    <router-link to="/projects">管理项目</router-link>
    <!-- <HelloWorld :tasks="tasks"/> -->
    <router-view :tasks="tasks" :projects="projects" />
  </div>
</template>

<script>
export default {
  name: "App",
  data() {
    return {
      projects:'',
      tasks:'',
    }
  },
  created(){
    
  }
};
</script>

<style>
* {
  list-style: none;
  margin: 0;
  padding: 0;
  text-decoration: none;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
