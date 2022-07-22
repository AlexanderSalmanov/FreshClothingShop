$(document).ready(function(){
    // ASYNC SEARCH

    var searchForm = $('.search-form')
    var searchInput = searchForm.find("[name='q']")
    var searchBtn = searchForm.find("[type='submit']")
    var typingTimer;
    var typingInterval = 1000;

    function DoSearch(){
      changeBtn()
      var query = searchInput.val()
      window.location.href = '/search/?q=' + query
    }

    function changeBtn(){
      searchBtn.addClass('disabled')
      searchBtn.html('<img style="height: 15px; width: 15px" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAYAAAA7MK6iAAAABmJLR0QA/wD/AP+gvaeTAAABDElEQVRIie2VTRLBMBxH31i4Ba6jOIerqCP52BkzygGMraoDtIadWiQGbdpKJGXhzWTRfMzL/5dMCn9+lD5wAELAq1McAqls+zo3VSYuG8vR0BQPeVQ11Fz7FiaxeXL+HuiairViM0E3aufYiK0DzIETMAPadrZWzZzHcaXAtC5xkhHHz4OqM25jJ5ZVxXdOepGt9aG4g4g3ASZUFHMXny2ItWl9Q2qDJjAGjkAE+LLPOT6vtzmVfW+zBBYG4kghjrKTyp7Mq1yUZQCsES/SGvFDcc6AfDVpRq6KevSpeFMgDp7mNKU8wuLligvEcdkiFbq/xV1B/1ZXrEsfdcU91+K7PEC8wUFd0j/G3AAp/mwHwV+puwAAAABJRU5ErkJggg=="/>Searching...')
    }

    searchInput.keyup(function(event){
      clearTimeout(typingInterval);
      typingTimer = setTimeout(DoSearch, typingInterval);
    })

    searchInput.keydown(function(event){
      clearTimeout(typingInterval);
    })








})
