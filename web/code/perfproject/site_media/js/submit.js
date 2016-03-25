var pageStates = Object.freeze({
    "INITIAL":0, 
    "SUBMITTED":1, 
    "PERIODIC":2
})

var state = pageStates.INITIAL

var ExampleApplication = React.createClass({
    getInitialState: function() {
        return {
        content: 'Testing Fetch',
        };
    },
    componentDidMount: function() {
        $.ajax({
          url: this.props.source,
          success: function(data) {
            this.setState({content: data});
            if(data=="No Servers"){
                alert("No available Rasberry Pi 2's, please wait a moment and resubmit");
            }
            else{
                state = pageStates.PERIODIC;
                React.render(
                    <p>Running code please be patient</p>,
                    document.getElementById('title'));
                document.title = "CSCI540 | Running Code";
            }
          }.bind(this)
        });
    },
    render: function() {
        return (
          <div>
            {this.state.content}
          </div>
        );
    }  
});

var gradeApplication = React.createClass({
    getInitialState: function() {
        return {
        content: 'Getting Performance Score',
        };
    },
    render: function() {
        
        return (
          <div>
            {this.state.content}
          </div>
        );
    }  
});


var HelloWorld = React.createClass({
  render: function() {
    return (
      <p>
        Hello, <input type="text" placeholder="Your name here" />!
        It is {this.props.date.toTimeString()}
      </p>
    );
  }
});




var CircularProgress = React.createClass({
    getDefaultProps: function() {
        return {
            r: 50,
            percentage: 50,
            strokeWidth: 1
        };
    },
    getInitialState: function() {
        return {
            percentage: parseInt(this.props.percentage, 10),
            r: this.props.r - this.props.strokeWidth / 2
        };
    },
    render: function() {
        var width = this.props.r * 2,
            height = this.props.r * 2,
            viewBox = "0 0 " + width + " " + height,
            dashArray = this.state.r * Math.PI * 2,
            dashOffset = dashArray - dashArray * this.props.percentage / 100;

        return (
            <svg
                className="CircularProgress"
                width={this.props.r * 2}
                height={this.props.r * 2}
                viewBox={viewBox}>
                <circle
                    className="CircularProgress-Bg"
                    cx={this.props.r}
                    cy={this.props.r}
                    r={this.state.r}
                    strokeWidth={this.props.strokeWidth + "px"} />
                <circle
                    className="CircularProgress-Fg"
                    cx={this.props.r}
                    cy={this.props.r}
                    r={this.state.r}
                    strokeWidth={this.props.strokeWidth + "px"}
                    style={{
                        strokeDasharray: dashArray,
                        strokeDashoffset: dashOffset
                    }} />
                    <text
                        className="CircularProgress-Text"
                        x={this.props.r}
                        y={this.props.r}
                        dy=".4em"
                        textAnchor="middle">{this.props.percentage + "%"}</text>
            </svg>
        );
    }
});



var InputDemo = React.createClass({
    getInitialState: function() {
        return {
            percentage: this.props.per
        };
    },
    render: function() {
        return (
            <div className="Percentage">
                <div>
                <h2>Percentage Complete</h2>
                </div>
                <CircularProgress
                    strokeWidth="10"
                    r="80"
                    percentage={this.props.per}/>
            </div>
        );
    }
});

var splitText = React.createClass({
    getInitialState: function() {
        return {
            data: this.props.data
        };
    },
    render: function() {
        {this.props.data.text.split("\n").map(function(item) {
          return (
            <span>
              {item}
              <br/>
            </span>
          )
        })};
        return (
            <div className="Percentage">
                <div>
                <h2>Percentage Complete</h2>
                </div>
                <CircularProgress
                    strokeWidth="10"
                    r="80"
                    percentage={this.props.per}/>
            </div>
        );
    }
});


/*React.render(<InputDemo/>,
    document.getElementById('container'));*/


var percentage = 0;




React.render(
  <ExampleApplication source="/server" />,
  document.getElementById('container')
);



update = setInterval(function() {
    if(state==pageStates.PERIODIC){
      $.ajax({
      url: "/wupdate",
      success: function(data) {
        
        if(data == "Stop"){
            clearInterval(update);
            $.ajax({
              url: "/grade",
              success: function(data) {
                  //var d = data;           
                  React.render(
                    <p>Graded Results</p>,
                    document.getElementById('title'));
                  document.title = "CSCI540 | Finished"; 
                  if(data=="ERROR"){
                      React.render(
                      <div>Something went wrong.</div>,
                    document.getElementById('container'));
                  }
                  else{
                      React.render(
                          <div id="grades">{ data }</div>,
                          document.getElementById('container')
                        );
                  }
                  
                  
                           
              }.bind(this)
            });
        }
        else{
            React.render(
            <InputDemo per={parseInt(data)}/>,
                document.getElementById('container'));
        }
      }.bind(this),
      
    });

    }
}, 500);
/*var start = new Date().getTime();

setInterval(function() {
  React.render(
    <ExampleApplication elapsed={new Date().getTime() - start} />,
    document.getElementById('container')
  );
}, 50);*/
