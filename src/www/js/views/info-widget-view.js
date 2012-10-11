/* Info Widget
* ====================== */

var InfoWidget = BaseWidget.extend({

  initialize : function() {  

    this.Name = "Info Widget"

    this.init()
    this.updateFrequency = 5000 // every 5 seconds
        
    // templates
    var templateSource        = $("#info-widget-template").html()
      , infoTemplateSource    = $("#info-template").html() 

    this.template         = Handlebars.compile(templateSource)
    this.infoTemplate     = Handlebars.compile(infoTemplateSource)
  }
  
, render: function() {

    var model         = this.model.toJSON()
      , markUp        = this.template(model.data[0])
      , infoMarkup    = this.infoTemplate(model.data[0])

    $(this.el).html(markUp)
      
    $('#spot').popover({
                               "title" : "info"
                            , "content" : infoMarkup
                            , "placement" : "bottom"
                             })

    $('#y1').popover({
                              "title" : "info"
                            , "content" : infoMarkup
                            , "placement" : "bottom"
                            })      
    $('#y3').popover({
                              "title" : "info"
                            , "content" : infoMarkup
                            , "placement" : "bottom"
                            })      
  }

})
