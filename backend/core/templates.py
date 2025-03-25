device_html = """
    <div class="card" style="width: 18rem;">
      <img class="card-img-top" src="..." alt="Card image cap">
      <div class="card-body">
        <h5 class="card-title">{{ device.name }}</h5>
        <p class="card-text">{{ device.description }}</p>
            
        {% for button in device.buttons %}    
             {{button.meta_button.html}}
        {% endfor %}
      </div>
    </div>
"""

meta_button_html = """
    <button class="btn btn-primary">
          {{ button.name }}
    </button>
"""
