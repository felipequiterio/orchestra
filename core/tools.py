from pydantic import BaseModel, Field
from typing import Callable, Dict, Any, Optional, get_type_hints
import inspect
from typing_extensions import get_args, get_origin

class BaseTool(BaseModel):
    name: str = Field(..., description="Tool name")
    description: str = Field(..., description="Tool description")
    
class Tool(BaseTool):
    """Base class for all tools with automatic parameter extraction"""
    
    def run(self, **kwargs) -> Any:
        """Method to be implemented by concrete tools"""
        raise NotImplementedError
    
    def get_schema(self) -> Dict[str, Any]:
        """Get OpenAI-style function schema for the tool"""
        parameters = self._get_parameters()
        
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": parameters,
                "required": [
                    name for name, info in parameters.items()
                    if info.get("required", True)
                ]
            }
        }
    
    def _get_parameters(self) -> Dict[str, Any]:
        """Extract parameters in OpenAI function schema format"""
        signature = inspect.signature(self.run)
        type_hints = get_type_hints(self.run)
        
        parameters = {}
        for name, param in signature.parameters.items():
            if name == 'self':
                continue
                
            param_type = type_hints.get(name, Any)
            param_info = self._get_parameter_info(name, param_type, param)
            parameters[name] = param_info
            
        return parameters
    
    def _get_parameter_info(self, name: str, param_type: Any, param: inspect.Parameter) -> Dict[str, Any]:
        """Get parameter info in OpenAI schema format"""
        # Handle Optional types
        is_optional = False
        if get_origin(param_type) is Optional:
            is_optional = True
            param_type = get_args(param_type)[0]
        
        # Get base parameter info
        param_info = {
            "type": self._get_type_str(param_type),
            "description": self._get_param_doc(name)
        }
        
        # Add default if exists
        if param.default != inspect.Parameter.empty:
            param_info["default"] = param.default
        
        # Add enum values if applicable
        if hasattr(param_type, "__members__"):  # Enum class
            param_info["enum"] = list(param_type.__members__.keys())
        
        return param_info
    
    def _get_type_str(self, type_hint: Any) -> str:
        """Convert Python type to JSON schema type"""
        type_map = {
            str: "string",
            int: "integer",
            float: "number",
            bool: "boolean",
            list: "array",
            dict: "object"
        }
        return type_map.get(type_hint, "string")
    
    def _get_param_doc(self, param_name: str) -> str:
        """Extract parameter description from docstring"""
        docstring = inspect.getdoc(self.run)
        if not docstring:
            return f"Parameter: {param_name}"
            
        lines = docstring.split('\n')
        for line in lines:
            if f"{param_name}:" in line:
                return line.split(':', 1)[1].strip()
        return f"Parameter: {param_name}"
