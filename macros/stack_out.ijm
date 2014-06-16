
// * stack_out.ijm
// *
// * ImageJ macro: Map merge
// *
// * Joaquin Correa, Data and Analytics services
// * JoaquinCorrea@lbl.gov
// * National Energy Research Scientific Computing Center
// * Lawrence Berkeley National Laboratory
// * 2013
// *
// * ImageJ macro to merge segmented files into a single file
// *

stack_dir=getArgument();
list = getFileList(stack_dir);

run("Image Sequence...", "open=" + stack_dir + " number=" + list.length + " starting=1 increment=1 scale=100 file=[] sort use");
saveAs("Tiff", stack_dir + "segmented_map.tif");
close();

//print("Done")