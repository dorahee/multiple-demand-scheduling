<html>
<head lang="en">
	<meta charset="UTF-8">
	<title></title>

	<!--
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css">
	<link rel="stylesheet" href="https://bootswatch.com/united/bootstrap.min.css">
	<link rel="stylesheet" type="text/css" href="//cdn.datatables.net/1.10.7/css/jquery.dataTables.css">
	<link rel="stylesheet" type="text/css" href="apps/results.css">
	<link rel="stylesheet" type="text/css" href="apps/colorbrewer.css">
	-->
	<link rel="stylesheet" type="text/css" href="apps/bootstrap.min.css">
	<link rel="stylesheet" type="text/css" href="apps/jquery.dataTables.css">
	<link rel="stylesheet" type="text/css" href="apps/results.css">
	<link rel="stylesheet" type="text/css" href="apps/colorbrewer.css">

	<!--
	<script src="https://code.jquery.com/jquery-1.11.3.min.js"></script>
	<script type="text/javascript" charset="utf8" src="//code.jquery.com/jquery-1.10.2.min.js"></script>
	<script type="text/javascript" charset="utf8" src="//cdn.datatables.net/1.10.7/js/jquery.dataTables.js"></script>
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"></script>
	<script src="http://d3js.org/d3.v3.min.js"></script>
	<script src="https://d3js.org/d3-queue.v3.min.js"></script>
	-->
	<script type="text/javascript" charset="utf8" src="apps/jquery-1.10.2.min.js"></script>
	<script type="text/javascript" charset="utf8" src="apps/jquery.dataTables.js"></script>
	<script src="apps/bootstrap.min.js"></script>
	<script src="apps/d3.v3.min.js"></script>
	<script src="apps/d3-queue.v3.min.js"></script>
	<script src="apps/colorbrewer.js"></script>
	<script src="apps/results.js"></script>


</head>
<body>

    <div id="divLoading">
    </div>
	<div class="container-fluid" id="top-container">
		<div role="tabpanel">
			<!--ul class="nav nav-tabs" role="tablist" -->
			<div class="col-xs-4">
				<select class="input-small form-control" id="selectionDropdown">
					<?php
					$target = 'results/';
					$weeds = array('.', '..');
					$directories = array_diff(scandir($target), $weeds);
					arsort($directories);

					$folders = [];

					foreach ($directories as $value) {
						if (is_dir($target . $value)) {
						    $sub_dirs = array_diff(scandir($target . $value), $weeds);
						    arsort($sub_dirs);
						    foreach ($sub_dirs as $sub_dir) {
                                    $path_subdir = $target . $value . "/" . $sub_dir;

									?>
									<option value="<?php echo $path_subdir; ?>"><?php echo substr($path_subdir, 8); ?></option>
									<?php
							}
						}
					}
					?>
				</select>
			</div>
			<div  class="col-xs-6">
				<ul class="nav nav-pills" role="tablist">
					<li role="presentation"><a href="#data" aria-controls="data" role="tab" data-toggle="tab">Research Overview</a></li>
					<li role="presentation"><a href="#lookup" aria-controls="lookup" role="tab" data-toggle="tab">Price Table</a></li>
					<li role="presentation"><a href="#table" aria-controls="table" role="tab" data-toggle="tab">Results</a></li>
					<li role="presentation" class="active"><a href="#heatmap" aria-controls="heatmap" role="tab" data-toggle="tab">Visualisation</a></li>
					<li role="presentation"><a href="#anaylsis" aria-controls="anaylsis" role="tab" data-toggle="tab">Graphs</a></li>
				</ul>
			</div>

			<div class="tab-content">
				<div role="tabpanel" class="tab-pane" id="data"> <?php include('apps/overview.php');?> </div>
				<div role="tabpanel" class="tab-pane" id="lookup"> <?php include('apps/lookup.php');?> </div>
				<div role="tabpanel" class="tab-pane" id="table"> <?php include('apps/results.php');?> </div>
				<div role="tabpanel" class="tab-pane active" id="heatmap"> <?php include('apps/visualisation.php');?> </div>
				<div role="tabpanel" class="tab-pane" id="anaylsis"></div>
			</div>
		</div>
	</div>

</body>

<!--
<footer class='site-footer'>
	<div class="container-fluid" id="footer-container">
		<div class="row">
			<div class="col-xs-3">Residential Electricity Demand Optimisation</div>
			<div class="col-xs-3">Faculty of Information Technology, Monash University</div>
			<div class="col-xs-6">Contact information: <a href="mailto:shan.he@monash.edu">Shan.He@monash.edu</a>, <a href="mailto:Ariel.Liebman@monash.edu">Ariel.Liebman@monash.edu</a>, <a href="mailto:Mark.Wallace@monash.edu">Mark.Wallace@monash.edu</a></div>
		</div>
	</div>
</footer>
-->
</html>

<script>
		$(document).ready(function () {
			var date = "15-06-02";
			var time = "15.48";
			var directory = "results/" + date + "/";
			var file = directory + date + "_" + time + ".json";
			var tabs_activated = [];

			var $dropDown = $("#selectionDropdown");

			var tab_active = $('.nav-pills .active a').attr("href");
			tabs_activated.push(tab_active);

			$dropDown.change(function () {
			    $("body").css('opacity', 0.4);
			    $("div#divLoading").addClass('show');
				showData($dropDown.val(), tab_active);
//				about();
			});

            $("body").css('opacity', 0.4);
			$("div#divLoading").addClass('show');
			showData($dropDown.val(), tab_active);
//			about();

            $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
                var target = $(e.target).attr("href"); // activated tab
                if (!tabs_activated.includes(target)) {
                    tabs_activated.push(target);
                    showData($dropDown.val(), target);
                }
            });

		});
	</script>