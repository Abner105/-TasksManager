// 弹窗组件
<template>
  <div>
    <button @click="show = true" :class="['title', 'iconfont']">
      &#xe651; {{ btntext }}
    </button>
    <div class="wrapper" v-show="show">
      <div class="alertp">
        <i class="iconfont">&#xe6f4;</i>
        <h3>{{ hint }}</h3>
        <input
          type="text"
          v-model="msg"
          :placeholder="hint"
          @keyup.enter="sclick(msg)"
          v-focus="true"
        />
        <button @click="sclick(msg)">确 定</button>
        <button @click="show = false">取 消</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "AlertPane",
  // 设置父组件传入的个性值
  props: {
    btntext: {
      type: String,
      default: "",
    },
    hint: {
      type: String,
      default: "请输入",
    },
  },
  data() {
    return {
      show: false, // 用于判断是否显示弹窗
      msg: "",
    };
  },
  methods: {
    // 弹窗组件中的“确定”点击事件
    sclick(msg) {
      let m = msg.trim();
      if (m) {
        this.$emit("itemclick", m);
      }
      this.show = false;
      // 将输入框中的内容清空
      this.msg = "";
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
@import url("//at.alicdn.com/t/font_2891783_979wkmq3c87.css");

.title {
  display: inline-block;
  color: #5fc6f1;
  font-size: 18px;
  font-weight: 600;
  vertical-align: middle;
  padding: 10px;
}
.title:hover {
  color: #00b3ff;
}
.wrapper {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.3);
}
.alertp {
  width: 250px;
  height: 165px;
  top: 280px;
  left: 45%;
  position: fixed;
  background-color: #fff;
  border-radius: 5px;
}
.alertp i {
  display: inline;
  padding-left: 10px;
  font-weight: 100;
  color: #4cbae9;
  font-size: 16px;
}
.alertp h3 {
  margin: 10px;
  height: 30px;
  line-height: 30px;
  display: inline-block;
  padding: 0 5px;
  font-size: 16px;
  font-weight: 900;
}
.alertp input {
  border-radius: 4px;
  width: 200px;
  height: 40px;
  border: solid #585c5e 1px;
  display: block;
  padding: 0 10px;
  margin: 3px auto;
  font-size: 14px;
}
.alertp button {
  border: #4cbae9 solid 1px;
  width: 70px;
  height: 35px;
  border-radius: 4px;
  color: #4cbae9;
  font-size: 14px;
  margin-top: 15px;
  margin-left: 35px;
}
.alertp button:hover {
  background-color: #4cbae9;
  color: #fff;
}
</style>
