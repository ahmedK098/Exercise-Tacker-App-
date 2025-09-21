// Function to add ordinal suffixes (st, nd, rd, th) to numbers
function addOrdinalSuffix(n) {
  const s = ["th", "st", "nd", "rd"];
  const v = n % 100;
  return n + (s[(v - 20) % 10] || s[v] || s[0]);
}

// Use d3.csv to load the data from the output.csv file
d3.csv("output.csv").then(data => {

  // Filter the data to show only the last 5 days
  const latestData = data.slice(-5);

  // Parse the date strings and numeric values
  const parseDate = d3.timeParse("%Y-%m-%d");
  latestData.forEach(d => {
    d.Date = parseDate(d.Date);
    d["Correct Rep count"] = +d["Correct Rep count"];
    d["Incorrect Rep Count"] = +d["Incorrect Rep Count"];
  });

  // Set up the SVG dimensions and margins
  const margin = { top: 20, right: 30, bottom: 40, left: 50 };
  const width = 600 - margin.left - margin.right;
  const height = 400 - margin.top - margin.bottom;

  // Append the SVG object to the body of the page
  const svg = d3.select("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  // Define the scales
  const x = d3.scaleTime()
    .domain(d3.extent(latestData, d => d.Date))
    .range([0, width]);

  const y = d3.scaleLinear()
    .domain([0, d3.max(latestData, d => Math.max(d["Correct Rep count"], d["Incorrect Rep Count"]))])
    .range([height, 0]);

  // Define the date format for the axis labels
  const formatDate = d3.timeFormat("%b");

  // Add the x-axis with a custom tick format to show only one label per day
  svg.append("g")
    .attr("transform", `translate(0,${height})`)
    .call(d3.axisBottom(x)
      .ticks(latestData.length)
      .tickFormat(d => `${formatDate(d)} ${addOrdinalSuffix(d.getDate())}`)
    );

  // Add the y-axis
  svg.append("g")
    .call(d3.axisLeft(y));

  // Add the "Correct Rep count" line
  const correctLine = d3.line()
    .x(d => x(d.Date))
    .y(d => y(d["Correct Rep count"]));

  svg.append("path")
    .datum(latestData)
    .attr("class", "line-correct")
    .attr("d", correctLine);

  // Add the "Incorrect Rep Count" line
  const incorrectLine = d3.line()
    .x(d => x(d.Date))
    .y(d => y(d["Incorrect Rep Count"]));

  svg.append("path")
    .datum(latestData)
    .attr("class", "line-incorrect")
    .attr("d", incorrectLine);

  // Add a legend
  const legend = svg.append("g")
    .attr("transform", `translate(${width - 120}, ${margin.top})`);

  // Correct Reps Legend
  legend.append("rect")
    .attr("x", 0)
    .attr("y", 0)
    .attr("width", 10)
    .attr("height", 10)
    .style("fill", "steelblue");
  legend.append("text")
    .attr("x", 15)
    .attr("y", 9)
    .text("Correct Reps")
    .style("font-size", "12px");

  // Incorrect Reps Legend
  legend.append("rect")
    .attr("x", 0)
    .attr("y", 20)
    .attr("width", 10)
    .attr("height", 10)
    .style("fill", "firebrick");
  legend.append("text")
    .attr("x", 15)
    .attr("y", 29)
    .text("Incorrect Reps")
    .style("font-size", "12px");
});