const buttonClose = document.getElementById('closeClick')
const message = document.getElementById('message')

if (message) {
  setTimeout(() => {
    buttonClose.click()
  }, 2000);
}