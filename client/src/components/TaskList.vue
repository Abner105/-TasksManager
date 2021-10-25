// 任务列表组件
<template>
  <div class="tasks">
    <div class="title">
      <h2>
        <i class="iconfont">&#xe6f4;</i>
        {{ pname }}
        <span>-- 任务列表</span>
        </h2>
      <!-- 引入弹窗组件，并监听弹窗中的确定事件 -->
      <alert-pane
        @itemclick="fclick"
        :btntext="'添加任务'"
        :hint="'请输入任务内容'"
      ></alert-pane>
    </div>
    <div v-if="stasks[0]">
      <ul>
        <li v-for="task in stasks" :key="task.id">
          <div :class="['task',task.condition]">
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
            <span>{{ task.date }}</span>
            <button @click="done(task.id)" v-if="task.condition == 'todo'">
              完成
            </button>
            <button @click="toptask(task.id)">置顶</button>
            <button @click="deltask(task.id)">删除</button>
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
    projects: {
      type: Array,
      default() {
        return [];
      },
    },
  },
  data() {
    return {
      sprojects: this.projects,
      stasks: this.tasks,
      pid: this.fpid,
      ischose: 0,
      focusstatus: false,
    };
  },
  computed: {
    pname() {
      let res = this.sprojects.filter((item) => item.id == this.pid)[0];
      if (res) {
        return  res.name;
      } else {
        return "";
      }
    },
  },
  watch: {
    tasks(val) {
      this.stasks = val;
    },
    fpid(val) {
      this.pid = val;
    },
    projects(val) {
      this.sprojects = val;
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
          data: { id: t.id, title: e.target.value },
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
.tasks {
  width: 700px;
  height: 600px;
  background-color: rgb(247, 247, 247);
  padding: 40px 20px;
  box-sizing: border-box;
  margin-top: 50px;
}
.title{
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  padding-right: 20px;
}
.tasks .title h2 {
  display: inline-block;
  font-size: 32px;
  font-weight: 900;
}
.title i{
  font-size: 30px;
  color: #4cbae9;
  font-weight: 100;
}
.title span{
  font-size: 20px;
  font-weight: 500;

}
.task{
  margin-top: 10px;
  width: 650px;
  height: 50px;
  background-color: rgb(138, 230, 102);
}
.done {
  color: #ddd;
  text-decoration: line-through #333;
}

</style>
