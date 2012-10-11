var RegionList = Backbone.View.extend({

  initialize : function() {       
    this.$el.empty()
    this.model.on("change", this.render, this)    
    this.$el.on("change", this.RegionChanged)
    this.model.fetch()   
  }

, RegionChanged : function(){
    $(document).trigger("RegionChange", $(this).val())   
}

, render : function() {
    var model = this.model.toJSON()   
      , self = this  

    $.each(model.regions,function(index, obj){
      if( obj.id == "us-east" )
        self.$el.append("<option value='" + obj.id + "' selected='selected'>" + obj.id + "</option>")
      else
        self.$el.append("<option value='" + obj.id + "'>" + obj.id + "</option>")
    })

    self.$el.trigger("change")
  }

})
