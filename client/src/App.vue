<template>
  <div id="app">
    <project-list
      :projects="projects"
      :fpid="fpid"
      @refresh="fswitch"
    ></project-list>
    <task-list :fpid="fpid" :tasks="tasks"></task-list>
  </div>
</template>

<script>
import axios from "axios";
import ProjectList from "./components/ProjectList.vue";
import TaskList from "./components/TaskList.vue";
export default {
  name: "App",
  components: {
    ProjectList,
    TaskList,
  },
  data() {
    return {
      projects: [],
      tasks: [],
      fpid: 1,
    };
  },
  methods: {
    // 子组件切换项目
    fswitch(e) {
      this.fpid = e;
      axios({
        method: "post",
        url: "http://127.0.0.1:5000/gettasks",
        data: { id: this.fpid },
      }).then((res) => {
        this.tasks = res.data;
      });
    },
  },
  // 获取初始值
  created() {
    // 获取项目
    axios({
      method: "post",
      url: " http://127.0.0.1:5000/getprojects",
    }).then((res) => {
      if (res.data[0]) {
        console.log(res.data);
        this.projects = res.data;
        this.fpid = res.data[0].id;
        // 获取第一个项目的任务列表
        axios({
          method: "post",
          url: "http://127.0.0.1:5000/gettasks",
          data: { id: this.fpid },
        }).then((res) => {
          this.tasks = res.data;
        });
      }
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
  margin: 60px auto;
  width: 500px;
  height: 600px;
  display: flex;
  flex-direction: row;
  justify-content: space-around;
}
</style>
