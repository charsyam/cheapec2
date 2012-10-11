var CategoryList = Backbone.View.extend({

  initialize : function() {       
    this.$el.empty()
    this.model.on("change", this.render, this)    
    this.$el.on("change", this.CategoryChanged)
    this.model.fetch()   
  }

, CategoryChanged : function(){
    $(document).trigger("CategoryChange", $(this).val())   
    $(document).trigger("SizeChange", $(this).val())
    $(document).trigger("ModelChange", $(this).val())
}

, render : function() {
    var model = this.model.toJSON()   
      , self = this  

    $.each(model.categories,function(index, obj){
        if( obj.id == "hiMemSpot" )
            self.$el.append("<option value='" + obj.id + "' selected='selected'>" + obj.id + "</option>")
        else
            self.$el.append("<option value='" + obj.id + "'>" + obj.id + "</option>")
    })

    self.$el.trigger("change")
  }

})
