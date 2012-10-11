var SizeList = Backbone.View.extend({

  initialize : function() {       
    this.$el.empty()
    this.model.on("change", this.render, this)    
    this.$el.on("change", this.SizeChanged)
    var self = this

    $(document).on("CategoryChange", function(e, category){
            self.category = category
            self.UpdateChanged()
    })
}

, UpdateChanged : function(){
    this.model.fetch({
        data : {
            category : this.category
        }
    })
}

, SizeChanged : function(){
    $(document).trigger("SizeChange", $(this).val())   
}

, render : function() {
    var model = this.model.toJSON()   
      , self = this  

    self.$el.empty()
    this.$el.on("sizechange", this.SizeChanged)

    $.each(model.sizes,function(index, obj){
      self.$el.append("<option value='" + obj.id + "'>" + obj.id + "</option>")
    })

    self.$el.trigger("change")
  }

})
