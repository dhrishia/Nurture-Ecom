var product_overview = $('#vertical');
 if(product_overview.length){
  product_overview.lightSlider({
    gallery:true,
    item:1,
    vertical:true,
    verticalHeight:450,
    thumbItem:3,
    slideMargin:0,
    speed:600,
    autoplay: true,
    responsive : [
      {
          breakpoint:991,
          settings: {
              item:1,
              
            }
      },
      {
          breakpoint:576,
          settings: {
              item:1,
              slideMove:1,
              verticalHeight:350,
            }
      }
  ]
  });  
 }
    



 