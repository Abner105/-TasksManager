<template>
  <div id="app">
    <!-- 引入两个前端路由 -->
    <router-link to="/tasks">任务列表</router-link>
    <router-link to="/projects">管理项目</router-link>
    <!-- 向子组件传入数据，并监听子组件中的addproject事件 -->
    <router-view :tasks="tasks" :projects="projects" @addproject="refresh"/>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "App",
  data() {
    return {
      projects: [],
      tasks: [],
    };
  },
  methods:{
    // 获取子组件传递的项目列表
    refresh(p){
      this.projects = p
    }
  },
  // 获取初始值
  created() {
    // 获取项目
    axios({
      method: "post",
      url: " http://127.0.0.1:5000/getprojects",
    }).then((res) => {
      this.projects = res.data;
      // 获取任务列表，默认获取第一个项目的任务列表
      axios({
        method: "post",
        url: "http://127.0.0.1:5000/gettasks",
        data: {id:res.data[0].id},
      }).then((res) => {
        this.tasks = res.data;
      });
    });
  },
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
