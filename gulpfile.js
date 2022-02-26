const gulp = require( 'gulp' );
const del = require( 'del' );

// ignore file. blender addon directory. ex. /Applications/Blender.app/Contents/Resources/2.93/scripts/addons/three-connector'
const { outDir } = require('./gulpOut');

const srcDir = './src';

function copy( c ){
	
	gulp.src( [ srcDir + '/**/*' ] ).pipe( gulp.dest( outDir ) );
	
	c();
	
}

function clean( c ){

	del( 
		[ outDir ],
		{
			force: true,
		} 
	).then( (paths) => {

		c();

	} );

}

function watch(){

	gulp.watch( srcDir + '/**/*' , gulp.series( copy ) );
	
}

exports.default = gulp.series( 
	clean,
	copy,
	watch
);