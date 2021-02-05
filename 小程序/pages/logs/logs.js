// logs.js
const util = require('../../utils/util.js')

Page({
  data: {
    queueSuc:false,
  },
  onLoad() {
    this.setData(
      {
        queueSuc:true,
      }
    )
  },

  queuecancel: function(){
    wx.navigateBack();
  },
  queuegoto: function(){
    wx.navigateTo({
      url: '../logs/logs'
    })
  }

})
