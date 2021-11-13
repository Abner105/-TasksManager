<template>
  <div id="app">
    <project-list
      :projects="projects"
      :fpid="fpid"
      @refresh="fswitch"
      @getproject="getproject"
    ></project-list>
    <task-list :fpid="fpid" :tasks="tasks" :projects="projects"></task-list>
  </div>
</template>

<script>
import ProjectList from "./components/ProjectList.vue";
import TaskList from "./components/TaskList.vue";
import {getTasks,getProjects} from "./network/api.js"
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
      // 未封装前直接使用axios框架，显得代码是否臃肿，缺少灵活性
      // axios({
      //   method: "post",
      //   url: "http://127.0.0.1:5000/gettasks",
      //   data: { id: this.fpid },
      // })
      getTasks(this.fpid).then((res) => {
        this.tasks = res.data;
      });
    },
    // 获取子组件传入的项目列表
    getproject(e){
      this.projects=e
    }
  },
  // 获取初始值
  created() {
    // 获取项目
    getProjects().then((res) => {
      if (res.data[0]) {
        this.projects = res.data;
        this.fpid = res.data[0].id;
        // 获取第一个项目的任务列表
        getTasks(this.fpid).then((res) => {
          this.tasks = res.data;
        });
      }
    });
  },
};
</script>

<style>
@import url('./assets/reset.css');
@import url('//at.alicdn.com/t/font_2891783_5kmbwvq7hv8.css');
#app {
  background-color: #fff;
  margin: 20px auto;
  width: 1000px;
  height: 700px;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}
</style>
