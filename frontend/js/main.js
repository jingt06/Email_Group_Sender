(function(){

	angular.module("email_sender",[])
		.controller("MainController",["$scope","$http",
			function($scope,$http){
				var init = function(){
					iFrameOn();
				}
				$scope.bold = function(){
					richTextField.document.execCommand('bold',false,null); 
				}

				$scope.underline = function(){
					richTextField.document.execCommand('underline',false,null)
				}

				$scope.italic = function(){
					richTextField.document.execCommand('italic',false,null)
				}

				$scope.size = function(size){
					richTextField.document.execCommand('FontSize',false,size)
				}

				$scope.color = function(color){
					richTextField.document.execCommand('ForeColor',false,color)
				}

				$scope.align_right = function(){
					richTextField.document.execCommand('justifyRight',false,null)
				}

				$scope.align_center = function(){
					richTextField.document.execCommand('justifyCenter',false,null)
				}

				$scope.align_left = function(){
					richTextField.document.execCommand('justifyLeft',false,null)
				}

				$scope.backgroundcolor = function(color){
					richTextField.document.execCommand('hilitecolor',false,color)
				}

				$scope.link = function(){
					var linkURL = prompt("Enter the URL for this link:", "http://"); 
					richTextField.document.execCommand("CreateLink", false, linkURL);
				}

				$scope.unlink = function(){
					richTextField.document.execCommand("Unlink", false, null);
				}

				$scope.ordered_list = function(){
					richTextField.document.execCommand("InsertOrderedList", false,"newOL");
				}

				$scope.unordered_list = function(){
					richTextField.document.execCommand("InsertUnorderedList", false,"newUL");
				}

				$scope.image = function(){
					var imgSrc = prompt('Enter image location', '');
				    if(imgSrc != null){
				        richTextField.document.execCommand('insertimage', false, imgSrc); 
				    }
				}

				$scope.horizontal = function(){
					richTextField.document.execCommand('inserthorizontalrule',false,null);
				}

				$scope.send_email = function(){
					html = window.frames['richTextField'].document.body.innerHTML;
					console.log(html)
					document.getElementById("preview").innerHTML=html;
				}

				function iFrameOn(){
					richTextField.document.designMode = 'On';
				}



				init();
			}
			])
}());