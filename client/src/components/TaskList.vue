// 任务列表组件
<template>
  <div class="tasks">
    
    <div v-if="Boolean(projects[0])">
      <select name="" id="" @change="switchProject" v-model="pid">
        <option
          v-for="project in projects"
          :key="project.id"
          :value="project.id"
        >
          {{ project.name }}
        </option>
      </select>
      <ul>
        <li v-for="task in t" :key="task.id" :class="task.condition">
          <div class="task">
            <h2>
              <!-- <input type="text" :value="task.title"> -->
              {{ task.title }}
              <button @click="done(task.id)" v-if="task.condition == 'todo'">
                完成
              </button>
              <button @click="toptask(task.id)">置顶</button>
              <button @click="deltask(task.id)">删除</button>
            </h2>
            <span>{{ task.date }}</span>
          </div>
        </li>
      </ul>
      <!-- 引入弹窗组件，并监听弹窗中的确定事件 -->
      <alert-pane @itemclick="fclick"></alert-pane>
    </div>
    <div v-else>暂无数据</div>

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
    fpid: {
      type: Number,
      default: 1,
    },
  },
  data() {
    return {
      t: this.tasks,
      pid: this.fpid,
    };
  },
  watch: {
    tasks(val) {
      this.t = val;
    },
    fpid(val) {
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
    // 监听点击完成按钮，完成任务
    done(tid) {
      axios({
        method: "post",
        url: "http://127.0.0.1:5000/done",
        data: { id: tid, pid: this.pid },
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
    // 删除任务
    deltask(tid) {
      axios({
        method: "post",
        url: "http://127.0.0.1:5000/deltask",
        data: { id: tid },
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
    // 置顶任务
    toptask(tid) {
      axios({
        method: "post",
        url: "http://127.0.0.1:5000/toptask",
        data: { id: tid, pid: this.pid },
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
  text-decoration: line-through #333;
}
</style>
