// 任务列表组件
<template>
  <div class="tasks">
    <div class="title">
      <h2>
        <i class="iconfont">&#xe6f4;</i>
        <h3>{{ pname }}</h3>
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
      <ul class="wrapper">
        <li v-for="(task, i) in stasks" :key="task.id">
          <div :class="['task', task.condition]">
            <i :class="['iconfont', color(i)]">&#xe629;</i>
            <h3
              @click="chose(task.id)"
              v-show="ischose != task.id"
              :title="task.title"
            >
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
            <button @click="deltask(task.id)" class="iconfont del">
              &#xe724;
            </button>
            <button
              @click="toptask(task.id)"
              class="iconfont top"
              v-if="task.condition == 'todo'"
            >
              &#xe610;
            </button>

            <button
              @click="done(task.id)"
              v-if="task.condition == 'todo'"
              class="iconfont complete"
            >
              &#xe64b;
            </button>
          </div>
        </li>
      </ul>
    </div>
    <div v-else class="nothing">
      <img src="../assets/nothing.png" alt="" />
      <h3>暂 无 数 据 , 请 先 添 加 任 务</h3>
    </div>
  </div>
</template>

<script>
import AlertPane from "./AlertPane.vue";
import { addTask, getTasks, done, delTask,topTask,alterTask } from "../network/api.js";
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
      clist: ["pink", "blue", "orange", "green", "tomato"],
    };
  },
  computed: {
    pname() {
      let res = this.sprojects.filter((item) => item.id == this.pid)[0];
      if (res) {
        return res.name;
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
    // 圆环创建不同的颜色
    color(i) {
      if (i > 4) {
        i = i % 5;
      }
      return this.clist[i];
    },
    // 添加任务并刷新任务列表(监听弹窗中的确定事件)
    fclick(title) {
      addTask(title, this.pid).then(() => {
        getTasks(this.pid).then((res) => {
          this.stasks = res.data;
        });
      });
    },
    // 完成任务(监听点击完成按钮)
    done(tid) {
      done(tid, this.pid).then(() => {
        getTasks(this.pid).then((res) => {
          this.stasks = res.data;
        });
      });
    },
    // 删除任务
    deltask(tid) {
      delTask(tid).then(() => {
        getTasks(this.pid).then((res) => {
          this.stasks = res.data;
        });
      });
    },
    // 置顶任务
    toptask(tid) {
      topTask(tid,this.pid).then(() => {
        getTasks(this.pid).then((res) => {
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
      // 如果值相等，不发送请求
      if (t.title != e.target.value) {
        alterTask(t.id,e.target.value).then(() => {
          getTasks(this.pid).then((res) => {
            this.stasks = res.data;
          });
        });
      }
    },
  },
  // 自定义获取焦点属性
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
  background-color: rgb(248, 248, 248);
  padding: 40px 30px;
  box-sizing: border-box;
  margin-top: 50px;
}
.title {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  padding: 0 0 10px 10px;
  width: 630px;
  /* background-color: antiquewhite; */
}
.title h3 {
  display: inline-block;
  max-width: 410px;
  /* background-color: antiquewhite; */
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.tasks .title h2 {
  display: inline-block;
  font-size: 24px;
  font-weight: 900;
}
.title i {
  font-size: 24px;
  color: #4cbae9;
  font-weight: 100;
  /* vertical-align:top ; */
  line-height: 38px;
}
.title span {
  font-size: 14px;
  font-weight: 500;
}
.wrapper {
  height: 500px;
  width: 665px;
  overflow-y: auto;
}
.task {
  margin-top: 12px;
  width: 635px;
  height: 50px;
  background-color: rgb(235, 235, 235);
  border-radius: 4px;
  /* overflow-x:hidden; */
}
.task:hover {
  /* background-color: #4cbae9; */
  transform: translateY(-1px);
  box-shadow: 0px 1px 6px rgba(0, 0, 0, 0.3);
  transition: 0.1s;
}
.task .pink {
  color: pink;
}
.task .blue {
  color: rgb(155, 155, 240);
}
.task .orange {
  color: rgb(255, 194, 81);
}
.task .tomato {
  color: tomato;
}
.task .green {
  color: rgb(129, 255, 129);
}
.task .iconfont {
  display: inline-block;
  width: 30px;
  height: 50px;
  line-height: 50px;
  padding-left: 15px;
  font-size: 16px;
  vertical-align: top;
}
.del:hover {
  color: rgb(255, 74, 74);
  font-weight: 900;
}
.top:hover {
  color: #2ea5d8;
  font-weight: 900;
}
.complete:hover {
  color: rgb(85, 218, 24);
  font-weight: 900;
}
.task .iconfont:first-child {
  font-weight: 900;
}
.task h3,
.task input {
  display: inline-block;
  width: 390px;
  height: 50px;
  font-size: 16px;
  line-height: 50px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  /* margin: 0!important; */
}
/* .task h3{
  overflow:hidden;
} */
.task span {
  display: inline-block;
  padding-right: 15px;
  vertical-align: top;
  line-height: 50px;
  margin-left: 10px;
}
.task.done {
  color: rgb(187, 187, 187);
}
.task.done .iconfont:first-child {
  color: rgb(187, 187, 187);
}
.task.done h3 {
  text-decoration: line-through rgb(116, 116, 116);
}
.nothing {
  width: 450px;
  height: 350px;
  /* background-color: antiquewhite; */
  margin: 30px auto;
  text-align: center;
}
.nothing img {
  width: 250px;
  margin: 20px auto;
  display: block;
}
.nothing h3 {
  margin-top: 50px;
  font-size: 16px;
}
</style>
