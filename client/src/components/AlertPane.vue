// 弹窗组件
<template>
<div>
  <button @click="show=true">添加</button>
  <div class="wrapper" v-show="show">
    <div class="alertp">
      <input type="text" v-model="msg" placeholder="请输入"/>
      <button @click="sclick(msg)">确定</button>
      <button @click="show=false">取消</button>
    </div>
  </div>
</div>
</template>

<script>
export default {
  name: "AlertPane",
  data(){
    return {
      show:false, // 用于判断是否显示
      msg:''
    }
  },
  methods:{
    // 弹窗组件中的“确定”点击事件
    sclick(msg){
      this.$emit('itemclick',msg)
      this.show = false
      // 将输入框中的内容清空
      this.msg = ''
    }
  }
};
</script>

<style scoped>
.wrapper {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.2);
}
.alertp {
  width: 200px;
  height: 100px;
  top: 200px;
  left: 45%;
  position: fixed;
  background-color: #fff;
}
.alertp input {
  margin:30px auto 10px;
}

</style>
