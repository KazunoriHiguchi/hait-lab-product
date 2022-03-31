'use strict';

function previewFile(hoge){
  var fileData = new FileReader();
  fileData.onload = (function() {
    //id属性が付与されているimgタグのsrc属性に、fileReaderで取得した値の結果を入力することで
    //プレビュー表示している
    document.getElementById('preview').src = fileData.result;
  });
  fileData.readAsDataURL(hoge.files[0]);
}