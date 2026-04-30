<script setup lang="ts">
import { onLaunch, onShow, onHide } from "@dcloudio/uni-app";
onLaunch(() => {
  console.log("App Launch");
});
onShow(() => {
  console.log("App Show");
});
onHide(() => {
  console.log("App Hide");
});
</script>
<style lang="scss">
/*每个页面公共css */

/* 重置 button 默认样式，避免各平台表现不一致 */
button {
  margin: 0;
  padding: 0;
  background: none;
  border: none;
  font-size: inherit;
  color: inherit;
  text-align: inherit;
  box-sizing: border-box;
  display: flex;
  align-items: center;
  justify-content: center;

  &::after {
    border: none;
  }
}
</style>
