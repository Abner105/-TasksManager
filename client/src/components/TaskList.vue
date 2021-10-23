// 任务列表组件
<template>
  <div class="tasks">
    <h2>任务列表</h2>
    <!-- 引入弹窗组件，并监听弹窗中的确定事件 -->
    <alert-pane
      @itemclick="fclick"
      :btntext="'+添加任务'"
      :hint="'请输入任务内容'"
    ></alert-pane>
    <div v-if="stasks[0]">
      <ul>
        <li v-for="task in stasks" :key="task.id" :class="task.condition">
          <div class="task">
            <h3 @click="chose(task.id)" v-show="ischose != task.id">
              {{ task.title }}
            </h3>
            <input
              v-show="ischose == task.id"
              type="text"
              :value="task.title"
              v-focus="focusstatus"
              id="input"
              @blur="altertask(task, $event)"
              @keyup.enter="altertask(task, $event)"
            />
            <button @click="done(task.id)" v-if="task.condition == 'todo'">
              完成
            </button>
            <button @click="toptask(task.id)">置顶</button>
            <button @click="deltask(task.id)">删除</button>
            <span>{{ task.date }}</span>
          </div>
        </li>
      </ul>
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
    fpid: {
      type: Number,
      default: 1,
    },
  },
  data() {
    return {
      stasks: this.tasks,
      pid: this.fpid,
      ischose: 0,
      focusstatus: false,
    };
  },
  watch: {
    tasks(val) {
      this.stasks = val;
    },
    fpid(val) {
      this.pid = val;
    },
  },
  methods: {
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
          this.stasks = res.data;
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
          this.stasks = res.data;
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
          this.stasks = res.data;
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
          this.stasks = res.data;
        });
      });
    },
    // 切换为输入框,并自动获取焦点
    chose(id) {
      this.ischose = id;
      this.focusstatus = true;
      const obj = document.getElementById("input");
      obj.selectionStart = obj.value.length;
      obj.selectionEnd = obj.value.length;
    },
    // 修改任务
    altertask(t, e) {
      this.ischose = 0;
      this.focusstatus = false;
      if (t.title != e.target.value) {
        axios({
          method: "post",
          url: "http://127.0.0.1:5000/altertask",
          data: { id: t.id , title:e.target.value},
        }).then((res) => {
          axios({
            method: "post",
            url: "http://127.0.0.1:5000/gettasks",
            data: { id: this.pid },
          }).then((res) => {
            this.stasks = res.data;
          });
        });
      }
    },
  },
  directives: {
    focus: {
      update: function (el, { value }) {
        if (value) {
          el.focus();
        }
      },
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
