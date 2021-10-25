<template>
  <div id="app">
    <project-list
      :projects="projects"
      :fpid="fpid"
      @refresh="fswitch"
      @getproject="getp"
    ></project-list>
    <task-list :fpid="fpid" :tasks="tasks" :projects="projects"></task-list>
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
    getp(e){
      this.projects=e
    }

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
@import url('./assets/reset.css');
@import url('//at.alicdn.com/t/font_2891783_ll23ld0syb.css');
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
