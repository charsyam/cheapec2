/* Main App
* ====================== */

var App = {

    init: function() {

        this.RegisterPartials()
        this.RegisterHelpers()

        var RegionDropDown = new RegionList({            
            el : $("#region-list")
          , model : new RegionListModel()
        })

        var CategoryDropDown = new CategoryList({            
            el : $("#category-list")
          , model : new CategoryListModel()
        })

        var SizeDropDown = new SizeList({            
            el : $("#size-list")
          , model : new SizeListModel()
        })

        var priceWidget = new PriceWidget({
            el : $("#price-widget-placeholder")
          , model : new PriceWidgetModel()
        })  

        var infoWidget = new InfoWidget({            
            el : $("#info-widget-placeholder")
          , model : new InfoWidgetModel()
        })
    }

  , RegisterPartials : function(){

       Handlebars.registerPartial("date-dropdown", $("#date-dropdown-template").html());

  } 

  , RegisterHelpers : function(){

    Handlebars.registerHelper('hash', function ( context, options ) {
  
              var ret = ""
                , counter = 0

              $.each(context, function ( key, value ) {
                
                if (typeof value != "object") {
                  obj = { "key" : key, "value" : value , "index" : counter++ }
                  ret = ret + options.fn(obj)
                }

              })

              return ret
    })

  }
}
