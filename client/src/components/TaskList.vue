// 任务列表组件
<template>
  <div class="tasks">
    <select name="" id="" @change="switchProject" v-model="pid">
      <option v-for="project in projects" :key="project.id" :value="project.id">
        {{ project.name }}
      </option>
    </select>
    <ul>
      <li v-for="task in t" :key="task.id" :class="task.condition">
        <div class="task">
          <h2>
            {{ task.title }}
            <button>完成</button>
            <button>修改</button>
            <button>删除</button>
          </h2>
          <span>{{ task.date }}</span>
        </div>
      </li>
    </ul>
    <!-- 引入弹窗组件，并监听弹窗中的确定事件 -->
    <alert-pane @itemclick="fclick"></alert-pane>
  </div>
</template>

<script>
import axios from "axios";
import AlertPane from "./AlertPane.vue";
export default {
  components: { AlertPane },
  name: "TaskList",
  // 获取父组件传递的数据：项目与初始化任务
  props: {
    tasks: {
      type: Array,
      default() {
        return [];
      },
    },
    projects: {
      type: Array,
      default() {
        return [];
      },
    },
  },
  data() {
    return {
      t: this.tasks,
      pid: this.projects[0].id,
    };
  },
  watch: {
    tasks(val) {
      this.t = val;
    },
    projects(val) {
      this.pid = val;
    },
  },
  methods: {
    // 监听切换项目，获取该项目下的任务
    switchProject() {
      axios({
        method: "post",
        url: "http://127.0.0.1:5000/gettasks",
        data: { id: this.pid },
      }).then((res) => {
        this.t = res.data;
      });
    },
    // 监听弹窗中的确定事件,添加任务并刷新任务列表
    fclick(title) {
      axios({
        method: "post",
        url: "http://127.0.0.1:5000/addtask",
        data: { title: title, pid: this.pid },
      }).then((res) => {
        axios({
          method: "post",
          url: "http://127.0.0.1:5000/gettasks",
          data: { id: this.pid },
        }).then((res) => {
          this.t = res.data;
        });
      });
    },
  },
};
</script>

<style scoped>
.done {
  color: #ddd;
}
</style>
