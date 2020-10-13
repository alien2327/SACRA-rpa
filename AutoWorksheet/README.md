SACRA 勤務表の自動化プロジェクト（RPA）
====

これは、SACRAの勤務表作成の自動化のためのプロジェクトです。

[Google Drive](https://drive.google.com/drive/u/3/folders/1VGCNctJvrtSEH3HFjZPfSUlr_f43Ltl-)

# 目標設定
    1．既存の勤務表ファイルの読み込み。
    2．これからの作成の自動化

# フォルダー構成
    /worksheet
        /worktaro
            /2019
                Jan_work.xlsx
                ...
                Dec_work.xlsx
            ...
        ...

# スクリプト設計
    1. osとsysでフォルダーとファイルを読み込む
    2. EXCELファイルの操作
    3. pandasでデータフレームの作成
    4. データベース化