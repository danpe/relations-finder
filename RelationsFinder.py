import sublime, sublime_plugin
import os

class RelationsFinderCommand(sublime_plugin.WindowCommand):
	def is_visible(self):
		view = self.window.active_view()
		fileName, fileExtension = os.path.splitext(view.file_name())
		return fileExtension == ".rb" and "ActiveRecord::Base" in view.substr(view.line(0))

	def run(self):
		view = self.window.active_view()
		regions = view.find_all("(belongs_to|has_many) :\w+")
		for region in regions:
			line = view.substr(region)
			if line.endswith('s'):
				line = line[:-1]
			model = line[line.index(":") + 1:] + ".rb"
			self.open_file_in_project(model)

	def open_file_in_project(self, file):
		root = self.window.folders()[0]
		for root, subFolders, files in os.walk(root):
			if file in files:
				self.window.open_file(os.path.join(root, file))