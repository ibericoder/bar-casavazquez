module.exports = {
    filenameHashing: true,
    configureWebpack: {
        output: {
            filename: 'js/[name].[hash].js',
            chunkFilename: 'js/[id].[chunkhash].js',
        },
    },
};
