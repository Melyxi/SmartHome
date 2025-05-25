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


mqtt_device_html = """
<h5 class="card-title">{{ device.name }}</h5>
<p class="card-text">{{ device.description }}</p>


<div class="col-xl-3 col-lg-4 col-sm-6 col-12 d-flex">
    <div class="flex-fill card flex-shrink-1">
<div class="card-body align-items-center row">
    {% for b in device.exposes %}

    {% if b["property"] == "water_leak" %}
        <div class="d-flex align-items-center">
             <div class="me-1"><i class="fa fa-fw fa-water"></i>
             </div>
             <div class="flex-shrink-1 flex-grow-1">Утечка воды</div>
             <div class="flex-shrink-1">
                 <div>
                 <strong id='{{device.unique_name}}_{{b["property"]}}'></strong>
                     <small class="text-muted ms-1">{{b["unit"]}}</small>
                 </div>
             </div>
         </div>
    {% elif b["property"] == "humidity" %}
            <div class="d-flex align-items-center">
                <div class="me-1"><i class="fa fa-fw text-info fa-tint"></i>
             </div>
             <div class="flex-shrink-1 flex-grow-1">Влажность</div>
             <div class="flex-shrink-1">
                 <div>
                 <strong id='{{device.unique_name}}_{{b["property"]}}'></strong>
                     <small class="text-muted ms-1">{{b["unit"]}}</small>
                 </div>
             </div>
         </div>
    {% elif b["property"] == "temperature" %}
            <div class="d-flex align-items-center">
             <div class="me-1"><i class="fa fa-fw text-danger fa-thermometer-half"></i>
             </div>
             <div class="flex-shrink-1 flex-grow-1">Температура</div>
             <div class="flex-shrink-1">
                  <div>
                 <strong id='{{device.unique_name}}_{{b["property"]}}'></strong>
                     <small class="text-muted ms-1">{{b["unit"]}}</small>
                 </div>
             </div>
         </div>
    {% elif b["property"] == "illuminance" %}
                <div class="d-flex align-items-center">
             <div class="me-1"><i class="fa fa-fw fa-sun"></i>
             </div>
             <div class="flex-shrink-1 flex-grow-1">Освещенность</div>
             <div class="flex-shrink-1">
                 <div>
                 <strong id='{{device.unique_name}}_{{b["property"]}}'></strong>
                     <small class="text-muted ms-1">{{b["unit"]}}</small>
                 </div>
             </div>
         </div>
    {% elif b["property"] == "soil_moisture" %}
                <div class="d-flex align-items-center">
             <div class="me-1"><i class="fa fa-fw fa-fill-drip"></i>
             </div>
             <div class="flex-shrink-1 flex-grow-1">Влажность почвы</div>
             <div class="flex-shrink-1">
                 <div>
                 <strong id='{{device.unique_name}}_{{b["property"]}}'></strong>
                     <small class="text-muted ms-1">{{b["unit"]}}</small>
                 </div>
             </div>
         </div>
    {% else %}
                <div class="d-flex align-items-center">
             <div class="me-1">
             </div>
             <div class="flex-shrink-1 flex-grow-1">{{b["label"]}}</div>
             <div class="flex-shrink-1">
                 <div>
                 <strong id='{{device.unique_name}}_{{b["property"]}}'></strong>
                     <small class="text-muted ms-1">{{b["unit"]}}</small>
                 </div>
             </div>
         </div>
    {% endif %}



        {% endfor %}
        <footer class="card-footer pt-0">
        <div class="row justify-content-between flex-nowrap">
            <div title="last update" class="col text-truncate">N/A</div>
            <div class="col col-auto text-truncate">
                <span class="me-1">
                    {% for b in device.exposes %}
                    {% if b["property"] == "linkquality" %}
                        <i class="fa fa-signal fa-fw"></i> <strong id='{{device.unique_name}}_{{b["property"]}}'></strong> LQI
                    {%endif%}
                    {% endfor %}
                </span><i class="fa fa-battery-three-quarters" title=""></i>
            </div>
        </div>
    </footer>
    </div>
        </div>
    </div>
 </div>
 </div>
"""


meta_button_html = """
    <button class="btn btn-primary">
          {{ button.name }}
    </button>
"""
